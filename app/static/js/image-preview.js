function setupRoomImagePreview() {
  const input = document.getElementById('room-images');
  const grid = document.getElementById('preview-grid');
  if (!input || !grid) return;

  let selectedFiles = [];

  const rebuildInputFiles = () => {
    const dt = new DataTransfer();
    selectedFiles.forEach((f) => dt.items.add(f));
    input.files = dt.files;
  };

  const render = () => {
    grid.innerHTML = '';
    if (!selectedFiles.length) {
      grid.style.display = 'none';
      return;
    }
    grid.style.display = 'grid';
    selectedFiles.forEach((file, idx) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const slot = document.createElement('div');
        slot.className = 'room-img-slot';
        slot.innerHTML = `
          <img src="${e.target.result}" alt="">
          <button type="button" class="remove-img" title="Bỏ"><i class="fas fa-times"></i></button>
        `;
        slot.querySelector('button')?.addEventListener('click', () => {
          selectedFiles = selectedFiles.filter((_, i) => i !== idx);
          rebuildInputFiles();
          render();
        });
        grid.appendChild(slot);
      };
      reader.readAsDataURL(file);
    });
  };

  input.addEventListener('change', () => {
    selectedFiles = Array.from(input.files || []).slice(0, 5);
    rebuildInputFiles();
    render();
  });
}

function setupAvatarPreview() {
  const avatarInput = document.getElementById('avatar-input');
  if (!avatarInput) return;
  avatarInput.addEventListener('change', function () {
    const file = this.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = document.getElementById('avatar-preview');
      if (img) img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  });
}

setupRoomImagePreview();
setupAvatarPreview();
