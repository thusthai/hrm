console.log('เซอุส บีเคเค');

//# สร้างการตรวจสอบข้อมูลก่อนการส่งด้วย submit (ในส่วนของ catset) เพื่อลดภาระงานของ back-end  
const MemberForm = document.querySelector('.member-form') ; 

function catsetValidation(event) {
    const checkCatSet = document.querySelectorAll('input[name="cat_set"]:checked'); //# จะได้ค่า checkCatSet ที่เป็น array # 1 - จำนวนทั้งหมดใน list
    if (checkCatSet.length === 0 ) {   //# ถ้าไม่มีการเลือกเลยจะได้ค่าเป็น 0
        event.preventDefault() ; //# ดักการทำงานของ submit form
        alert('กรุณาเลือกรายการที่ท่านสนใจอย่างน้อย 1 รายการ');
    }
    
}

if (!!MemberForm) {
   MemberForm.addEventListener('submit',catsetValidation); 
}


