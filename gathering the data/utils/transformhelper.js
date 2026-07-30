function extractBrand(item){
    return item.split(' ')[0];
}

function extractField(description, field) {
    const lines = description.split('\n');

    const line = lines.find(l => l.trim().startsWith(field));

    if (!line) return null;

    return line.split(':')[1]?.trim() || null;
}

function extractSpec(product, specName){
    if(!product || !product.attributes) return null;

    const x = product.attributes.find(a => a.name === specName);

    return x?.terms?.[0]?.name || null;
}

function cleanHTML(html){
    return html
      .replace(/<br\s*\/?>/gi, "\n")
      .replace(/<\/p>/gi, "\n")
      .replace(/<[^>]*>/g, "")
      .replace(/\n+/g, "\n")
      .trim();
  }


  function extract(lines, keyword){ 
    for(let i = 0; i < lines.length; i++){
      if(lines[i].includes(keyword)){
        return lines[i+1] || lines[i];
      }
    }
    return null;
  }
  
  function extractInline(lines, keyword){
    for(let i = 0; i < lines.length; i++){
      if(lines[i].includes(keyword)){
        return lines[i];
      }
    }
    return null;
  }

  function extractModel(name){
    if(!name) return null;
  
    const withoutBrand = name.split(" ").slice(1).join(" ");
  
    const model = withoutBrand.split(/,|–|-/)[0];
  
    return model.trim();
  }

module.exports = {extractBrand, extractField, extractSpec, cleanHTML, extract, extractInline, extractModel};

