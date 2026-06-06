document.addEventListener("DOMContentLoaded", () => {
  for (const textarea of document.querySelectorAll("textarea")) {
    textarea.addEventListener("input", () => {
      textarea.style.height = "auto";
      textarea.style.height = `${textarea.scrollHeight}px`;
    });
  }
});

