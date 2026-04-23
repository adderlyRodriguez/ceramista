(function () {
  const lightbox = document.getElementById('lightbox');
  if (!lightbox) return;

  const mediaBox = lightbox.querySelector('.lightbox-media');
  const titleEl = lightbox.querySelector('.lightbox-title');
  const metaEl = lightbox.querySelector('.lightbox-meta');
  const descEl = lightbox.querySelector('.lightbox-description');
  const closeBtn = lightbox.querySelector('.lightbox-close');

  function open(data) {
    mediaBox.innerHTML = '';
    if (data.type === 'video') {
      const v = document.createElement('video');
      v.src = data.url;
      v.controls = true;
      v.autoplay = true;
      v.playsInline = true;
      mediaBox.appendChild(v);
    } else {
      const img = document.createElement('img');
      img.src = data.url;
      img.alt = data.title || '';
      mediaBox.appendChild(img);
    }
    titleEl.textContent = data.title || '';
    const parts = [];
    if (data.category) parts.push(data.category);
    if (data.date) parts.push(data.date);
    metaEl.textContent = parts.join(' · ');
    descEl.textContent = data.description || '';

    lightbox.hidden = false;
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    const v = mediaBox.querySelector('video');
    if (v) v.pause();
    mediaBox.innerHTML = '';
    lightbox.hidden = true;
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  document.querySelectorAll('.media-trigger').forEach(function (el) {
    const handler = function () {
      open({
        type: el.dataset.type,
        url: el.dataset.url,
        title: el.dataset.title,
        description: el.dataset.description,
        category: el.dataset.category,
        date: el.dataset.date
      });
    };
    el.addEventListener('click', handler);
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        handler();
      }
    });
  });

  closeBtn.addEventListener('click', close);
  lightbox.addEventListener('click', function (e) {
    if (e.target === lightbox) close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !lightbox.hidden) close();
  });
})();
