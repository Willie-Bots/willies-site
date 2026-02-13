async function loadNewsletter() {
  const dateEl = document.getElementById('newsletterDate');
  const summaryEl = document.getElementById('newsletterSummary');
  const listEl = document.getElementById('newsletterList');

  try {
    const res = await fetch('./data/paymentsdive-newsletter.json?ts=' + Date.now());
    if (!res.ok) throw new Error('Could not load newsletter data');
    const data = await res.json();

    dateEl.textContent = data.generated_date || 'Today';
    summaryEl.textContent = data.summary || 'Latest PaymentsDive headlines.';
    listEl.innerHTML = '';

    (data.articles || []).forEach((a) => {
      const li = document.createElement('li');

      const link = document.createElement('a');
      link.href = a.link;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = a.title;

      const summary = document.createElement('p');
      summary.className = 'article-summary';
      summary.textContent = a.description || 'No summary available.';

      li.appendChild(link);
      li.appendChild(summary);
      listEl.appendChild(li);
    });
  } catch (err) {
    dateEl.textContent = 'Unavailable';
    summaryEl.textContent = 'Could not load today’s recap.';
    listEl.innerHTML = '';
  }
}

loadNewsletter();
