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

function notify_for_change_user_info() {
    if (confirm('Bạn có chắc chắn muốn thay đổi thông tin cá nhân?') == true){
         fetch('/change_info_user', {
        method: 'post'
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        if (data.code == 200){
            alert('success')
        }
        else if (data.code == 400){
            alert('fail')
        }
        location.reload()
    }).catch(err => console.error(err))
    }
}



sessionStorage.setItem("serial", 1);

var typeObject = {
        StoredProcedures: ["Name", "Definition", "Owner"],
        Tables: ["Name", "Definition", "Owner", "Schema"],
        Views: ["Name", "Definition", "Owner"]
    }
    window.onload = function () {
        var typeSel = document.getElementById("typeSel"),
            fieldSel = document.getElementById("fieldSel")
        for (var type in typeObject) {
            typeSel.options[typeSel.options.length] = new Option(type, type);
        }
        typeSel.onchange = function () {
            fieldSel.length = 1; // remove all options bar first
            if (this.selectedIndex < 1) return; // done
            var ft = typeObject[this.value];
            for (var field in typeObject[this.value]) {
                fieldSel.options[fieldSel.options.length] = new Option(ft[field], field);
            }
        }
        typeSel.onchange();
    }

  $('document').ready(function() {
  $('.add_another').click(function() {
      $("#table-thanh-toan-hoa-don").append('<tr><td></td><td></td><td></td><td></td><td></td><tr>');
   });
})

