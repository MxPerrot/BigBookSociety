document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("zoom-modal");
    const zoomedImg = document.getElementById("zoomed-img");
    const closeBtn = document.querySelector(".close");

    document.querySelectorAll(".media-scroller img").forEach(img => {
        img.addEventListener("click", function () {
            zoomedImg.src = this.src;
            modal.style.display = "flex";
        });
    });

    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    modal.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
});
