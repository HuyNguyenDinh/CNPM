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
        popup = document.querySelector('.popup_detail-pay-the-bill');
        popup.classList.add("show_popup_detail");
        if (data.code == 200){
            console.log('success');
        }
        else if (data.code == 400)
            console.log('fail');
    }).catch(err => console.error(err))

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

var med_list

function get_med_list_json() {
    fetch('/api/get_medicine', {
            method: 'post'
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            med_list = data
            temp("med-1", "med-unit-1")
        }).catch(err => console.error(err))
}

var elements = document.querySelectorAll('.pay-the-bill_unpaid');
elements.forEach(element => {
element.addEventListener('click',()=>{
    element.classList.add("pay-the-bill_paid");
    element.classList.remove("pay-the-bill_unpaid");
    })
})

function notify_for_change_user_info() {
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

sessionStorage.setItem("medicine", {})
sessionStorage.setItem("serial", 2);

function temp(med_id, med_unit_id) {
    var typeSel = document.getElementById(med_id),
        fieldSel = document.getElementById(med_unit_id);
    if (med_list != null) {
        for (const [key, value] of Object.entries(med_list)) {
            typeSel.options[typeSel.options.length] = new Option(value["name"], key);
        }
    }
    typeSel.onchange = function () {
        fieldSel.length = 1; // remove all options bar first
        if (this.selectedIndex < 1) return; // done
        var ft = med_list[this.value]["unit"];
        for (var field in med_list[this.value]["unit"]) {
            fieldSel.options[fieldSel.options.length] = new Option(ft[field]["tag"] + "-" + ft[field]["price"], field);
        }
    }
}


function add_row_for_med_bill() {
    med_id = "med-" + sessionStorage.getItem("serial")
    med_unit_id = "med-unit-" + sessionStorage.getItem("serial")
    $("#talbe2-chi-tiet-thanh-toan-hoa-don").append(`<tr><td>${sessionStorage.getItem("serial")}</td><td><select id=${med_id} size="1"><option value="" selected="selected">Select subject</option></select></td><td><select class="medicine-unit-id" id=${med_unit_id} size="1"><option value="" selected="selected">Please select subject first</option></select></td><td><input type="number" min="0" class="quantity" placeholder="Số lượng"></td><td><input type="text" class="use"></td></tr>`);
    temp(med_id, med_unit_id);
    sessionStorage['serial'] = sessionStorage['serial'] - 1 + 2
}

function create_medical_bill(user_id, patient_id, exam_date) {
    var unit_id = document.getElementsByClassName("medicine-unit-id");
    var quantity = document.getElementsByClassName("quantity");
    var diagnosis = $('textarea#diagnosis').val();
    var symptom = $('textarea#symptom').val();
    var use = document.getElementsByClassName("use");
    var total = {"user_id": user_id, "patient_id": patient_id, "exam_date": exam_date, "diagnosis" : diagnosis, "symptom" : symptom,"medicine": {}}
    for (var i = 0; i < unit_id.length; i++) {
        total["medicine"][unit_id[i].value] = {"quantity" : quantity[i].value, "use" : use[i].value}
    }
    fetch('/api/create-medical-bill', {
            method: 'post',
            body: JSON.stringify (total),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            popup = document.querySelector('.popup_detail-pay-the-bill');
            popup.classList.add("show_popup_detail");
            if (data.code == 200) {
                console.log('success')
            }
            else if (data.code == 400){
                console.log('fail')
            }
        }).catch(err => console.error(err))
}


