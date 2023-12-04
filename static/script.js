    const imgfrom = document.getElementById('updimg');
    const imginput = document.getElementById('input');
    const updimg = document.getElementById('imgupd');

    imgfrom.addEventListener("change", function (a) {
      a.preventDefault();
      const file = imginput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (a) {
          updimg.src = a.target.result;
        };
        reader.readAsDataURL(file);
      }
    });