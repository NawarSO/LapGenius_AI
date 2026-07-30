const dotenv = require('dotenv');
dotenv.config();

const {runAdapter} = require("./pipline.js");
const spacenetAdapter = require('./adapters/spacenet.js');
const afandyAndSpahyAdapter = require('./adapters/afandySpahy.js');
const laptopSy = require('./adapters/laptopSy.js');
const newLaptop = require('./adapters/new-laptop.js');
async function runPipelines() {
   try{
    let totalrows = 0;
    const adapters = [spacenetAdapter, afandyAndSpahyAdapter, laptopSy, newLaptop];
    for(const adapter of adapters){
        console.log(`Fetching the data ...`)
       const returned = await runAdapter(adapter);
       if(returned.length > 0){
        console.log(`Number rows data from ${returned[0].source} is: ${returned.length}`);
        totalrows += returned.length;
       } else{
        console.log(`No data fetched from ${adapter.name || 'unknown adapter'}`);
       }

    }
    console.log(`Number of rows fetched from all sites is ${totalrows}`);
}catch(error){
    console.error('An error happen while fetching the data runPipline fun... ', error.message);
}}

runPipelines();