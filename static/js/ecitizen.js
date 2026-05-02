// e-Citizen Kenya — Shared JavaScript Utilities

document.addEventListener('DOMContentLoaded', () => {
  // Enable htmx CSRF
  document.body.addEventListener('htmx:configRequest', (evt) => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
      evt.detail.headers['X-CSRFToken'] = csrfToken.value;
    }
  });

  // Status badge color updates via Alpine.js data
  Alpine.data('statusBadge', (status) => ({
    status,
    get colorClass() {
      const colors = {
        draft: 'bg-gray-100 text-gray-700',
        submitted: 'bg-blue-100 text-blue-700',
        in_review: 'bg-yellow-100 text-yellow-700',
        approved: 'bg-green-100 text-green-700',
        completed: 'bg-green-100 text-green-800',
        rejected: 'bg-red-100 text-red-700',
        pending: 'bg-yellow-100 text-yellow-700',
        processing: 'bg-blue-100 text-blue-700',
        failed: 'bg-red-100 text-red-700',
        cancelled: 'bg-gray-100 text-gray-500',
      };
      return colors[this.status] || 'bg-gray-100 text-gray-700';
    },
  }));
});
