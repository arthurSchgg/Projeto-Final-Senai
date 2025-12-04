document.addEventListener("DOMContentLoaded", function() {
    const toasts = document.querySelectorAll(".toast");

    toasts.forEach(toast => {
        const progress = toast.querySelector(".progress");
        const duration = 5000; // tempo total em ms
        let startTime = null;

        function animate(timestamp) {
            if (!startTime) startTime = timestamp;
            const elapsed = timestamp - startTime;
            const width = Math.max(100 - (elapsed / duration) * 100, 0);
            progress.style.width = width + "%";

            if (elapsed < duration) {
                requestAnimationFrame(animate);
            } else {
                toast.remove();
            }
        }

        requestAnimationFrame(animate);

        toast.querySelector(".btn-fechar").addEventListener("click", () => {
            toast.remove();
        });
    });
});
