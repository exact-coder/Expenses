const renderChat=(data,labels) =>{

    
    const ctx = document.getElementById('myChart');
      
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Last 6 months expenses',
          data: data,
          borderWidth: 1
        }]
      },
      options: {
        title: {
            display:true,
            text: "Expenses per Category",
        }
      }
    });
};
const getChatData=()=> {
    fetch("expense_category_summary").then((res) => res.json()).then((results) => {
        console.log(results);
        const category_data = results.expense_category_data;
        const [labels,data] = [Object.keys(category_data),Object.values(category_data),]

        renderChat(data,labels)
    });
}

document.onload=getChatData()