function submitForm() {
  document.querySelector('#createPost').submit();
}

function checkText() {
  document.getElementById("floatingTextarea").addEventListener("input", () => {
    var textarea = document.getElementById("floatingTextarea");
    var button = document.getElementById("submitButton");
    if (textarea.value.trim() !== "") {
      button.style.display = "block";
    } else {
      button.style.display = "none";
    }
  });
}

function likePost() {
  document.getElementById("like-post").addEventListener("click", () => {
    
  })
}
document.addEventListener('DOMContentLoaded', checkText)
