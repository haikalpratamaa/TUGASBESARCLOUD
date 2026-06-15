(function () {
  "use strict";

  // --- Sidebar toggle (mobile) ---
  var sidebarToggle = document.querySelector("[data-sidebar-toggle]");
  var sidebarOverlay = document.querySelector("[data-sidebar-overlay]");

  function closeSidebar() {
    document.body.classList.remove("sidebar-open");
  }

  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", function () {
      document.body.classList.toggle("sidebar-open");
    });
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener("click", closeSidebar);
  }

  // --- Flash auto-dismiss (5 detik) ---
  document.querySelectorAll("[data-auto-dismiss]").forEach(function (alert) {
    setTimeout(function () {
      dismissAlert(alert);
    }, 5000);
  });

  // --- Flash close button ---
  document.querySelectorAll("[data-dismiss-alert]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var alert = btn.closest(".alert");
      if (alert) {
        dismissAlert(alert);
      }
    });
  });

  function dismissAlert(el) {
    if (el.classList.contains("alert--dismiss")) return;
    el.classList.add("alert--dismiss");
    el.addEventListener("animationend", function () {
      el.remove();
    });
  }

  // --- Confirm modal ---
  var confirmModal = document.querySelector("[data-confirm-modal]");
  var confirmMessage = document.querySelector("[data-confirm-message]");
  var confirmAccept = document.querySelector("[data-confirm-accept]");
  var confirmCancel = document.querySelector("[data-confirm-cancel]");
  var pendingForm = null;

  document.querySelectorAll("[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      pendingForm = form;
      if (confirmMessage) {
        confirmMessage.textContent =
          form.dataset.confirm || "Apakah Anda yakin ingin melanjutkan?";
      }
      if (confirmModal) {
        confirmModal.hidden = false;
      }
    });
  });

  if (confirmCancel) {
    confirmCancel.addEventListener("click", function () {
      pendingForm = null;
      if (confirmModal) confirmModal.hidden = true;
    });
  }

  if (confirmAccept) {
    confirmAccept.addEventListener("click", function () {
      if (pendingForm) pendingForm.submit();
    });
  }

  // --- Loading state pada form submit ---
  document.querySelectorAll("form[data-loading]").forEach(function (form) {
    form.addEventListener("submit", function () {
      var btn = form.querySelector('button[type="submit"]');
      if (btn && !btn.classList.contains("is-loading")) {
        btn.classList.add("is-loading");
        btn.dataset.originalText = btn.textContent;
        btn.textContent = btn.dataset.loading || "Mengirim...";
      }
    });
  });
})();
