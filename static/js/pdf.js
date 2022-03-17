// js code to generate pdf of ticket

window.onload = function(){
    document.getElementById("download")
    .addEventListener("click",()=>{
        const ticket = this.document.getElementById("ticket");
        console.log(ticket);
        console.log(window);
        var opt = {
            filename : 'myTrainTicket.pdf',
        };
        html2pdf().from(ticket).set(opt).save();
    })
}