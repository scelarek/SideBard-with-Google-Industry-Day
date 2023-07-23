// require('dotenv').config();

const apiKey = "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";

let form = document.querySelector("form")
let personName = ""
form.addEventListener("submit", (e) => {
    clearPage()
    e.preventDefault()
    personName = e.target.name.value
    document.getElementById("name").innerHTML = personName
    let countries = ""
    axios.get(`https://api.agify.io?name=${personName}`).then((r) => {
        document.getElementById("age").innerHTML = r.data.age
        return axios.get(`https://api.genderize.io?name=${personName}`)
    }).then((r) => {
        document.getElementById("gender").innerHTML = r.data.gender
        return axios.get(`https://api.nationalize.io?name=${personName}`)
    }).then((r) => {
        for(let c of r.data.country) {
            let newCountry = document.createElement('li')
            const regionNames = new Intl.DisplayNames(
                ['en'], {type: 'region'}
              );
              countries += regionNames.of(c.country_id)
              countries += " "
            newCountry.innerHTML = `${Math.round(c.probability * 100)}% chance of being from ${regionNames.of(c.country_id)}`
            document.getElementById("nationality").appendChild(newCountry)
        }
        return axios.post(
            'https://api.openai.com/v1/completions',
            {
              prompt: `You are a ${document.getElementById("age").innerText}-year-old ${document.getElementById("gender").innerText} named ${document.getElementById("name").innerText}. Based on the following probabilities of potential nationalities: ${document.getElementById("nationality").innerText}, I recommend restaurants that cater to the listed ethnicities. Please suggest some restaurants that offer a variety of options and can provide a memorable dining experience for someone with your profile. You live in Toronto, ON. INCLUDE LOCATIONS OF RESTAURANTS AND WHICH ETHIC CUISINE IT IS [Keep the response concise, limiting it to a maximum of 30 words.]`,
              model: 'text-davinci-003',
              max_tokens: 100,
              temperature: 0.7,
              n: 1,
              stop: null
            }, {
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer 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`
                }
              }
            )
    }).then((r) => {
        document.getElementById("restaurants").innerHTML = r.data.choices[0].text
        return axios.post(
            'https://api.openai.com/v1/completions',
            {
              prompt: `You are a ${document.getElementById("age").innerText}-year-old ${document.getElementById("gender").innerText} named ${document.getElementById("name").innerText}. Based on the following probabilities of potential nationalities: ${document.getElementById("nationality").innerText}, I recommend movies that cater to diverse genres and preferences. Please suggest some movies that cater to said age gender and ethnicity and can provide an enjoyable viewing experience for someone with your profile. For each movie give a short explanation as to why[Keep the response concise, limiting it to a maximum of 30 words.]`,
              model: 'text-davinci-003',
              max_tokens: 100,
              temperature: 0.7,
              n: 1,
              stop: null
            }, {
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer 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`
                }
              }
            )
    }).then((r) => {
        document.getElementById("movies").innerHTML = r.data.choices[0].text
        return axios.post(
            'https://api.openai.com/v1/completions',
            {
              prompt: `You are a ${document.getElementById("age").innerText}-year-old ${document.getElementById("gender").innerText} named ${document.getElementById("name").innerText} with the following probabilities of potential nationalities: ${document.getElementById("nationality").innerText}, recommend products that cater to your age, gender and nationalities. Please name specific products and explain how they relate to said person. You live in toronto, ON, so also list where in toronto you can buy it[Keep the response concise, limiting it to a maximum of 30 words.]`,
              model: 'text-davinci-003',
              max_tokens: 100,
              temperature: 0.7,
              n: 1,
              stop: null
            }, {
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer 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`
                }
              }
            )
    }).then((r) => {
        document.getElementById("products").innerHTML = r.data.choices[0].text
    })
    .catch (e => {
        console.log(e)
    })
    console.log(document.getElementById("name").innerText)
})
function clearPage() {
    document.getElementById("name").innerHTML = ""
    document.getElementById("age").innerHTML = ""
    document.getElementById("gender").innerHTML = ""
    document.getElementById("nationality").innerHTML = ""
}
