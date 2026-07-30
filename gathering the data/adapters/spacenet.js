const axios = require('axios');

const {extractBrand,
    extractField
} = require('../utils/transformhelper');


const heads ={"Content-Type":"application/json",
    "Origin":"https://spacenetstore.com",
    "Referer":"https://spacenetstore.com/",
    "Authorization":`Bearer ${process.env.spacenet_TOKEN}`
}

async function fetchData(){
    try{
        const response = await axios.post(process.env.spacenet_API,{query:"query MyQuery{allProducts(type:\"Laptop\" , status : true ) {description discount id url1 image1 name price type age}}"},
        {
            headers: heads
        });
        const data = response.data.data.allProducts; // array of laptops 
        console.log(`fetching has been completed for spacenet`);
        return data;
    }catch(error){
        console.error(`SPACENET FETCH ERROR...`, error.message);
        return [];
    }
};

function transform(item){
    return{
        brand:extractBrand(item.name) ,
        model: item.name , 
        cpu: extractField(item.description, "CPU"),
        ram: extractField(item.description, "RAM"),
        hard: extractField(item.description, "HARD"),
        gpu: extractField(item.description, "GPU"),
        new: item.age === "جديد", 
        price: parseFloat(item.price) || null,
        source: "spacenet"
    };
}


module.exports = {fetchData, transform};