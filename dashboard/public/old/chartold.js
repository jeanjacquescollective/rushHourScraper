const randomColors = (count) => {
  let colors = [];
  let letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < count; i++) {
    color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    colors.push(color);
  }
  return colors;
};

const readTextFile = (file, callback) => {
  var rawFile = new XMLHttpRequest();
  rawFile.overrideMimeType('application/json');
  rawFile.open('GET', file, true);
  rawFile.onreadystatechange = function () {
    if (rawFile.readyState === 4 && rawFile.status == '200') {
      callback(rawFile.responseText);
    }
  };
  rawFile.send(null);
};

const makeCharts = async () => {
  const createChart = (poi) => {
    // const fileName = json.split('/').pop().split('.').shift();
    const fileName = poi.metaData.title;
    generateChart(poi.peakHours, fileName);
  };
  const datasetsFromData = (data) => {
    let datasets = [];
    let index = 0;
    for (let key in data) {
      if (key != 'hours') {
        datasets.push({
          data: data[key].map((x) => x[1]),
          fill: false,
          borderColor: colors[index++],
          label: key,
        });
      }
    }
    return datasets;
  };

  const generateChart = (data, fileName) => {
    let xValues = data['hours'];
    const id = createIDfromFileName(fileName);
    console.log(id);
    new Chart('' + id, {
      type: 'line',
      data: {
        labels: xValues,
        datasets: datasetsFromData(data),
      },
      options: {
        legend: {
          display: true,
          position: 'bottom',
        },
        title: {
          display: true,
          text: fileName,
          position: 'top',
        },
      },
    });
  };

  const createIDfromFileName = (fileName) => {
    return '' + fileName.split('/').pop().split('.').shift().replace(/ /g, '_');
  };
  const createElementForChart = (poi) => {
    console.log(poi);
    const id = createIDfromFileName(poi.metaData.title);
    const div = document.createElement('canvas');
    div.id = id;
    div.classList.add('card');
    div.style = 'width:100%;max-width:700px';
    document.querySelector('#main-charts-holder').appendChild(div);
  };

  // const files = fs.readdirSync('/js/json/');
  // console.log(files);
  const startApp = async (query, amount = 5) => {
    let loader = `<div class="loader"></div>`;
    document.getElementById('loading').innerHTML = loader;
    let response = await fetch(
      `http://127.0.0.1:8000/rushhours/${query}`
    );
    const jsonDataLinks = await response.json();
    console.log(jsonDataLinks.data);
    let jsonData = jsonDataLinks.data;
    for (let poi in jsonData) {
      createElementForChart(jsonData[poi]);

      createChart(jsonData[poi]);
    }
    document.getElementById('loading').innerHTML = '';
  };
  startApp("koffieshops gent");
  // old version with json files
  // jsonDataLinks.data.forEach(file => {
  //   readTextFile(file, function (text) {
  //     let data = JSON.parse(text);
  //     // console.log(data)
  //     for (let poi in data)
  //     {
  //       createElementForChart(data[poi]);

  //       createChart(data[poi]);
  //     }
  //   });

  // })
};
const colors = randomColors(7);

makeCharts();

export { makeCharts };
