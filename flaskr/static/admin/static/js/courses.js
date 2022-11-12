const enroll = document.querySelectorAll("#enroll-btn");

if (enroll.length !== 0) {
  enroll.forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      let response = await fetch(`/courses/enroll/${e.target.dataset.id}`);
      let data = await response.json();
      if (data.success) {
        btn.innerHTML = "Enrolled";
        btn.disabled = true;
      } else {
        console.log(data.success);
      }
    });
  });
}
