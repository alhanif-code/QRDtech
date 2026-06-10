let qrcode = ""
let filename = ""
let dropFile = null

const dropzone = document.getElementById('dropzone')
dropzone.addEventListener('dragover', (event) => {
    event.preventDefault()
})
dropzone.addEventListener('drop', (event) => {
    event.preventDefault()
    dropFile = event.dataTransfer.files[0]
})
document.getElementById('myuserfile').addEventListener('change', (event) => {
    dropFile = event.target.files[0]
})

function generateQR() {
    const name = document.getElementById("user").value
    const inputFilename = document.getElementById("filename").value
    const myuserfile = dropFile

    if (name === "" || inputFilename === "" || !myuserfile) {
        alert("please fill all")
        return
    }

    const formData = new FormData()
    formData.append('myuserfile', myuserfile)
    formData.append('filename', inputFilename)

    fetch('/upload', {
        method: 'POST',
        body: formData
    })

        .then(response => response.json())
        .then(data => {
            qrcode = data.qrcode
            filename = data.filename

            const img = document.getElementById('qrImage')
            img.src = 'data:image/png;base64,' + data.qrcode
        })
}

function downloadQR() {
    if (qrcode === "") {
        alert("Please generate a QR code first.")
        return
    }

    const link = document.createElement('a')
    link.href = 'data:image/png;base64,' + qrcode
    link.download = filename + '.png'
    link.click()
}
