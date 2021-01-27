const modal = document.querySelector('.modal');
const overlay = document.querySelector('.overlay');

const openModal = function(){
    modal.classList.remove('hidden');
    overlay.classList.remove('hidden');
};
document.querySelector('.sim').addEventListener('click',openModal);

const closeModal = function () {
    modal.classList.add('hidden');
    overlay.classList.add('hidden');
    $.ajax({
        url: "/",
        type: "get",
        success: function(response) {
            window.location.href = "/"
        },
    });
};
document.querySelector('.close-modal').addEventListener('click',closeModal);
overlay.addEventListener('click',closeModal);

document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
        closeModal();
    }
});
