let form = document.querySelector('button')

form.onsubmit = function (evt) {
    evt.preventDefault();
    alert('Вы нажали на кнопку 1');
}

// async function createGroup() {
//     alert('Вы нажали на кнопку 1');
//     // console.log("111");
// }
