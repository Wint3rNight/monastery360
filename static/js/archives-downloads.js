// Delegated handler for archive preview/download actions
(function () {
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-download-url]');
    if (!a) return;
    var url = a.dataset.downloadUrl;
    if (!url) return;
    if (a.dataset.preview === '1') {
      e.preventDefault();
      window.open(url + '?inline=1', '_blank', 'noopener');
      return;
    }
    // download action: ensure href is set so the browser can handle the download attribute
    if (a.dataset.action === 'download') {
      a.href = url;
      // remove target to let browser handle download attribute without new tab
      a.removeAttribute('target');
    }
  });
})();
