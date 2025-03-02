document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('#tabs button');
    const tabContents = document.querySelectorAll('.tab-content');
    const emailPreviews = document.querySelectorAll('.email-preview');
    const emailPreviewSection = document.getElementById('email-preview-section');
    const emailPreviewPlaceholder = document.querySelector('.email-preview-placeholder');

    let currentEmail = null;

    // Handle tab switching
    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            const tabId = this.getAttribute('data-tab');

            // Hide all tab contents
            tabContents.forEach(content => {
                content.classList.remove('active');
            });

            // Remove active class from all tabs
            tabs.forEach(t => {
                t.classList.remove('active');
            });

            // Show the selected tab content and mark the tab as active
            document.getElementById(tabId).classList.add('active');
            this.classList.add('active');
        });
    });

    // Set the first tab as active by default
    tabs[0].classList.add('active');

    // Handle email preview clicks
    emailPreviews.forEach(preview => {
        preview.addEventListener('click', function () {
            const emailId = this.getAttribute('data-email');
            const fullEmail = document.getElementById(emailId);

            if (currentEmail === emailId) {
                // If the same email is clicked again, hide the preview
                emailPreviewSection.innerHTML = '<div class="email-preview-placeholder">Click an email to preview it here.</div>';
                currentEmail = null;
                this.classList.remove('selected'); // Remove selected class
            } else {
                // Show the full email preview
                emailPreviewSection.innerHTML = fullEmail.innerHTML;
                currentEmail = emailId;

                // Remove selected class from all email previews
                emailPreviews.forEach(p => p.classList.remove('selected'));
                // Add selected class to the clicked email preview
                this.classList.add('selected');
            }
        });
    });
});