"""
python manage.py upload_to_r2

Uploads all files from local media/ to Cloudflare R2
under the websites/chatsargana/ prefix.
"""
import os
from pathlib import Path

import boto3
from botocore.client import Config
from django.conf import settings
from django.core.management.base import BaseCommand


MIME_MAP = {
    '.jpg':  'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png':  'image/png',
    '.webp': 'image/webp',
    '.gif':  'image/gif',
    '.svg':  'image/svg+xml',
}


class Command(BaseCommand):
    help = 'Upload local media/ files to Cloudflare R2'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be uploaded without doing it',
        )

    def handle(self, *args, **options):
        dry_run    = options['dry_run']
        media_root = Path(settings.BASE_DIR) / 'media'

        if not media_root.exists():
            self.stdout.write(self.style.WARNING('media/ folder not found - nothing to upload.'))
            return

        client = boto3.client(
            's3',
            endpoint_url=settings.R2_ENDPOINT,
            aws_access_key_id=settings.R2_ACCESS_KEY,
            aws_secret_access_key=settings.R2_SECRET_KEY,
            config=Config(signature_version='s3v4'),
            region_name='auto',
        )
        bucket = settings.R2_BUCKET
        prefix = 'websites/chatsargana'

        files = [f for f in media_root.rglob('*') if f.is_file()]

        if not files:
            self.stdout.write(self.style.WARNING('No files found in media/'))
            return

        self.stdout.write(f'Files to upload: {len(files)}')
        if dry_run:
            self.stdout.write(self.style.WARNING('[DRY RUN] - no actual upload'))

        ok = 0
        fail = 0
        for fpath in files:
            rel          = fpath.relative_to(media_root).as_posix()
            key          = f'{prefix}/{rel}'
            ext          = fpath.suffix.lower()
            content_type = MIME_MAP.get(ext, 'application/octet-stream')

            if dry_run:
                self.stdout.write(f'  [dry] {rel}  ->  {key}')
                ok += 1
                continue

            try:
                client.upload_file(
                    str(fpath),
                    bucket,
                    key,
                    ExtraArgs={'ContentType': content_type},
                )
                self.stdout.write(self.style.SUCCESS(f'  OK   {rel}'))
                ok += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  FAIL {rel}: {e}'))
                fail += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done: {ok} uploaded, {fail} failed'))
        if ok and not dry_run:
            self.stdout.write(f'Public URL base: {settings.R2_PUBLIC_URL}/{prefix}/')
