// SOLUCIÓN DEFINITIVA - MODALES
document.addEventListener('DOMContentLoaded', function() {
    // Configuración GLOBAL para todos los modales
    document.querySelectorAll('[data-bs-toggle="modal"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const modalId = this.getAttribute('data-bs-target');
            const modal = new bootstrap.Modal(document.querySelector(modalId), {
                backdrop: 'static',
                keyboard: false
            });
            modal.show();
        });
    });
    
    // Elimina TODOS los efectos hover
    document.querySelectorAll('*').forEach(el => {
        el.style.transition = 'none';
        el.style.transform = 'none';
    });
});
