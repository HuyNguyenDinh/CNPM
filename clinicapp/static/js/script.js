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
        if (data.code == 200)
            console.log('success')
        else if (data.code == 400)
            console.log('fail')
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