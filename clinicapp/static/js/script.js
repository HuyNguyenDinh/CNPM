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

            dis = document.getElementsByClassName("btn-thanh-toan")
            for (d of dis) {
                d.style.display = "none";
            }
            title_popup.innerHTML = "Lập phiếu khám thành công!";
            popup.style.border = '5px solid green';
            popup.classList.add("show_popup_detail");

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
function get_phone_number(obj){
    document.getElementById("last_name").disabled = true;
    document.getElementById("first_name").disabled = true;
    document.getElementById("sex").disabled = true;
    document.getElementById("date_of_birth").disabled = true;
    document.getElementById("date_of_exam").disabled = true;
    document.getElementById("button_submit").disabled = true;
    event.preventDefault()
    fetch('/api/check-phone-number', {
        method: 'post',
        body: JSON.stringify({
            'phone_number': obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res){
        console.log(res)
        return res.json()

    }).then(function(data){
        console.log(data)
        if (data.code == 200){
            if(confirm('Thông tin của bạn đã được lưu trên hệ thống!!!' +'\n' + 'Bạn có phải là '+ data.last_name +' '+ data.first_name + ' không?') == true){
                    document.getElementById("last_name").value = data.last_name;
                    document.getElementById("first_name").value = data.first_name;
                    document.getElementById("sex").value = data.sex;
                    document.getElementById("date_of_birth").value = data.date_of_birth;
                    document.getElementById("date_of_exam").disabled = false;
                    document.getElementById("button_submit").disabled = false;
            }
            else{
                    document.getElementById("phone_number").value = null;
                    document.getElementById("last_name").value = null;
                    document.getElementById("first_name").value = null;
                    document.getElementById("sex").value = 3;
                    document.getElementById("date_of_birth").value = null;
            }
        }
        else if(data.code == 300 && data.phone_number != ''){
            alert('Số điện thoại ' + data.phone_number + ' của bạn được ghi nhận đăng ký lần đầu trên hệ thống!!!')
            document.getElementById("last_name").disabled = false;
            document.getElementById("first_name").disabled = false;
            document.getElementById("sex").disabled = false;
            document.getElementById("date_of_birth").disabled = false;
            document.getElementById("date_of_exam").disabled = false;
            document.getElementById("button_submit").disabled = false;
        }
        else if(data.code == 400 && data.phone_number != ''){
            alert(data.error_ms)
        }
    }).catch(function(err){
        console.error(err)
    })
}

function get_pay_url_momo(bill_id, amount, current_url) {
    fetch('/api/pay_with_momo', {
        method: 'post',
        body: JSON.stringify ({
            'id': bill_id,
            'amount': amount,
            'current_url': current_url})
    }).then(function(res){
        console.log(res);
        return res.json();
    }).then.then(function(data) {
        console.log(data.code);
        if (data.code == 200) {
            console.log('success');
            window.location.replace(data.pay_url);
        }
        else if (data.code == 400) {
         console.log('fail');
        }
    }).catch(function(err) {
        console.error(err);
    });
}

function fix_loop(){
    document.getElementById("last_name").disabled = true;
    document.getElementById("first_name").disabled = true;
    document.getElementById("sex").disabled = true;
    document.getElementById("date_of_birth").disabled = true;
    document.getElementById("date_of_exam").disabled = true;
    document.getElementById("button_submit").disabled = true;
}
function api_medical_register(){
    event.preventDefault()
    var phone_number = document.getElementById("phone_number").value;
    var last_name = document.getElementById("last_name").value;
    var first_name = document.getElementById("first_name").value;
    var sex = document.getElementById("sex").value;
    var date_of_birth = document.getElementById("date_of_birth").value;
    var date_of_exam = document.getElementById("date_of_exam").value;
    console.log(last_name)
    fetch('/api/medical-register', {
        method: 'post',
        body: JSON.stringify({
            'phone_number': phone_number,
            'last_name': last_name,
            'first_name': first_name,
            'sex': sex,
            'date_of_birth': date_of_birth,
            'date_of_exam': date_of_exam
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res){
        console.info(res)
        return res.json()
    }).then(function(data){
        console.info(data)
        if (data.code == 400){
             alert(data.error_ms)
        }
        else if (data.code == 200){
            alert(data.error_ms)
        }

    )}.catch(function(err){
        console.error(err)
    })
}