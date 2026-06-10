let qrImageData = ""
let currentFilename = ""

function generateQR(){
    const name = document.getElementById("name").value
    const url = document.getElementById("url").value
    const filename = document.getElementById("filename").value

    if (name === "" || url === "" || filename === ""){
        alert("please fill all")
        return
    }

    fetch('/generate', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name : name,
            url : url,
            filename : filename
        })
    })

    .then(response => response.json())
    .then(data => {
        qrImageData = data.qr_code
        currentFilename = data.filename

        const img = document.getElementById("qrImage")
        img.src = 'data:image/png;base64,' + data.qr_code
    })
}

function downloadQR(){
    if (qrImageData === ""){
        alert("Please generate a QR code first.")
        return
    }

    const link = document.createElement('a')
    link.href = 'data:image/png;base64,' + qrImageData
    link.download = currentFilename + '.png'
    link.click()
}