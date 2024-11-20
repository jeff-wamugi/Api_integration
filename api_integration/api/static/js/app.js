fetch('http://127.0.0.1:8000/api/send-sms/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        phone: ['+254712345678'],
        message: 'Test message',
    }),
})
.then(response => response.json())
.then(data => console.log(data)) // handle successful response
.catch(error => console.error('Error:', error)); // handle errors
