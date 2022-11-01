function animateStatistics(){
  let statistics = document.querySelectorAll(".statistic");
  for(let statistic of statistics){
    let updateNumber = ()=>{
      let target =+ statistic.getAttribute("data-target");
      let number =+ statistic.innerText.replace(",","");
      let speed = 500;
      let increment = target/speed;
      if(number < target){
        statistic.innerText = Math.ceil(number+increment).toLocaleString();
        setTimeout(updateNumber,1);
      }
      else{
        statistic.innerText = target.toLocaleString();
      }
    }
    updateNumber();
  }
}

