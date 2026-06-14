/* ─── Inline Edit (admin in-page editing) ───────────────────
 * Activates only when window.IS_STAFF === true.
 * Recognised attributes:
 *   data-edit="model.pk.field"          (model: usagecard, herostat, …)
 *   data-sc="key_name"                  (SiteContent shortcut → sitecontent.<key>.value)
 * For text fields the element becomes contenteditable.
 * For image fields the element should wrap an <img>; a file picker overlay is shown.
 */
(function () {
  if (!window.IS_STAFF) return;

  const API = '/panel/api/inline/';

  // ─── CSRF ──
  function getCookie(name) {
    const m = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return m ? decodeURIComponent(m[2]) : '';
  }
  const csrftoken = getCookie('csrftoken');

  // ─── Parsing data attrs ──
  function parseEdit(el) {
    const ds = el.dataset.sc;
    if (ds) return { model: 'sitecontent', pk: ds, field: 'value' };
    const de = el.dataset.edit;
    if (!de) return null;
    const parts = de.split('.');
    if (parts.length < 3) return null;
    return { model: parts[0], pk: parts[1], field: parts.slice(2).join('.') };
  }

  // Field type guess (only image needs special UI; everything else = text)
  function isImageField(el) {
    return el.dataset.editType === 'image' || el.querySelector(':scope > img') !== null && el.dataset.edit && el.dataset.edit.endsWith('.image');
  }

  // ─── Toast ──
  function toast(msg, ok = true) {
    let t = document.getElementById('ie-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'ie-toast';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.className = 'ie-toast ' + (ok ? 'ie-ok' : 'ie-err');
    requestAnimationFrame(() => t.classList.add('ie-show'));
    clearTimeout(t._tm);
    t._tm = setTimeout(() => t.classList.remove('ie-show'), 2200);
  }

  // ─── Save call ──
  async function saveField({ model, pk, field }, value, file) {
    const fd = new FormData();
    fd.append('model', model);
    fd.append('pk', pk);
    fd.append('field', field);
    if (file) fd.append('value', file);
    else      fd.append('value', value);

    const r = await fetch(API, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      body: fd,
      credentials: 'same-origin',
    });
    const d = await r.json().catch(() => ({ ok: false, error: 'bad response' }));
    if (!r.ok || !d.ok) throw new Error(d.error || 'Алдаа гарлаа');
    return d;
  }

  // ─── Text editing ──
  function attachTextEdit(el) {
    const meta = parseEdit(el);
    if (!meta) return;

    el.classList.add('ie-target');

    const ui = document.createElement('div');
    ui.className = 'ie-ctl';
    ui.innerHTML =
      '<button type="button" class="ie-btn ie-edit-btn" title="Засах">✎</button>';
    el.appendChild(ui);

    const editBtn = ui.querySelector('.ie-edit-btn');

    editBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      enterEditMode(el, meta, ui);
    });
  }

  function enterEditMode(el, meta, ui) {
    if (el.classList.contains('ie-editing')) return;
    el.classList.add('ie-editing');

    // Hide control buttons inside element while editing
    const original = el.innerHTML;
    // Remove the control UI from the element so it isn't part of the editable text
    ui.remove();
    const originalText = el.innerText;
    el.setAttribute('contenteditable', 'true');
    el.focus();

    // Place caret at end
    const sel = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(el);
    range.collapse(false);
    sel.removeAllRanges();
    sel.addRange(range);

    const bar = document.createElement('div');
    bar.className = 'ie-ctl ie-ctl-bar';
    bar.contentEditable = 'false';
    bar.innerHTML =
      '<button type="button" class="ie-btn ie-save">Хадгалах</button>' +
      '<button type="button" class="ie-btn ie-cancel">Болих</button>';
    el.appendChild(bar);

    const cleanup = (restore) => {
      el.removeAttribute('contenteditable');
      el.classList.remove('ie-editing');
      bar.remove();
      if (restore) el.innerHTML = original;
      // Re-attach edit button
      el.appendChild(ui);
    };

    bar.querySelector('.ie-cancel').addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      cleanup(true);
    });

    bar.querySelector('.ie-save').addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      // Temporarily remove bar to read clean text
      bar.remove();
      const newText = el.innerText.trim();
      el.appendChild(bar);
      try {
        const d = await saveField(meta, newText);
        let saved = d.value != null ? d.value : newText;
        // Auto-format pure integers with thousand separators
        if (/^-?\d+$/.test(saved)) {
          saved = Number(saved).toLocaleString('en-US');
        }
        el.textContent = saved;
        toast('Хадгалагдлаа');
        cleanup(false);
      } catch (err) {
        toast(err.message || 'Алдаа', false);
      }
    });
  }

  // ─── Image editing ──
  function attachImageEdit(wrap) {
    const meta = parseEdit(wrap);
    if (!meta) return;
    wrap.classList.add('ie-target', 'ie-image-target');

    const ctl = document.createElement('div');
    ctl.className = 'ie-ctl ie-img-ctl';
    ctl.innerHTML =
      '<label class="ie-btn ie-img-pick">Зураг солих'
      + '<input type="file" accept="image/*" hidden></label>'
      + '<button type="button" class="ie-btn ie-save" disabled>Хадгалах</button>';
    wrap.appendChild(ctl);

    const fileInput = ctl.querySelector('input[type="file"]');
    const saveBtn   = ctl.querySelector('.ie-save');
    const img       = wrap.querySelector(':scope > img');

    let pickedFile = null;
    let originalSrc = img ? img.src : '';

    fileInput.addEventListener('change', () => {
      const f = fileInput.files && fileInput.files[0];
      if (!f) return;
      pickedFile = f;
      if (img) {
        const url = URL.createObjectURL(f);
        img.src = url;
      }
      saveBtn.disabled = false;
    });

    saveBtn.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!pickedFile) return;
      saveBtn.disabled = true;
      saveBtn.textContent = '...';
      try {
        const d = await saveField(meta, null, pickedFile);
        if (img && d.image_url) {
          img.src = d.image_url + '?t=' + Date.now();
          originalSrc = img.src;
        } else if (!img && d.image_url) {
          // Create the img if it didn't exist (icon-only card upgraded)
          const newImg = document.createElement('img');
          newImg.src = d.image_url;
          newImg.alt = '';
          wrap.insertBefore(newImg, wrap.firstChild);
        }
        toast('Зураг солигдлоо');
        pickedFile = null;
        saveBtn.textContent = 'Хадгалах';
      } catch (err) {
        if (img) img.src = originalSrc;
        toast(err.message || 'Алдаа', false);
        saveBtn.textContent = 'Хадгалах';
        saveBtn.disabled = false;
      }
    });
  }

  // ─── Init ──
  document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('ie-mode');

    document.querySelectorAll('[data-edit], [data-sc]').forEach((el) => {
      const ed = el.dataset.edit || '';
      if (ed.endsWith('.image') || el.dataset.editType === 'image') {
        attachImageEdit(el);
      } else {
        attachTextEdit(el);
      }
    });

    // Floating status badge
    const badge = document.createElement('div');
    badge.className = 'ie-badge';
    badge.innerHTML = '<span class="ie-dot"></span>Засварлах горим';
    document.body.appendChild(badge);
  });
})();
