const url = "http://127.0.0.1:8000/users/me"

async function getMyData(url) {
    const result = await fetch(url);
    console.log(result.json())
}

getMyData(url)