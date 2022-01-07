function pay_the_bill(bill_id) {
    fetch('/api/pay-bill', {
        method: 'post',
        body: JSON.stringify ({
            'id': bill_id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        console.log(data.code)

        if (data.code == 200){
            console.log('success');
        }
        else if (data.code == 400)
            console.log('fail');
    }).catch(err => console.error(err))
    popup = document.querySelector('.popup_detail-pay-the-bill');
    popup.classList.add("show_popup_detail");

}

function make_medical_list(exam_id) {
    fetch('/api/create-exam', {
        method: 'post',
        body: JSON.stringify ({
            'id': exam_id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        console.log(data.code)
        if (data.code == 200)
            console.log('success')
        else if (data.code == 400)
            console.log('fail')
        location.reload()
    }).catch(err => console.error(err))

}


const elements = document.querySelectorAll('.pay-the-bill_unpaid');
elements.forEach(element => {
element.addEventListener('click',()=>{
    element.classList.add("pay-the-bill_paid");
    element.classList.remove("pay-the-bill_unpaid");
    })
})

//Go to top
const mybutton = document.querySelector(".button-go-to-top");
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
  if (document.body.scrollTop > 40 || document.documentElement.scrollTop > 40) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
function topFunction() {
  document.documentElement.scrollTop = 0;

}