const loader = `<div class="loader"></div>`;
const loaderElement = document.getElementById('loading');
const sidebarElement = document.querySelector('.sidenav__list');
const chartListElement = document.querySelector('#main-charts-holder');
const randomColors = (numberOfColours) => {
  let colors = [];
  let letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < numberOfColours; i++) {
    color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    colors.push(color);
  }
  return colors;
};

const saveToStorage = (search, data) => {
  localStorage[search] = JSON.stringify(data);
};
const createElementForSidebar = (search) => {
  const element = document.createElement('a');
  element.classList.add('sidenav__list-item');
  const textElement = document.createElement('span');
  textElement.classList.add('sidenav__list-item-text');
  textElement.innerHTML = search;
  element.appendChild(textElement);
  const deleteElement = document.createElement('span');
  deleteElement.classList.add('delete');
  deleteElement.innerHTML = '🗑️';
  deleteElement.addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    localStorage.removeItem(search);
    sidebarElement.removeChild(element);
  });
  element.appendChild(deleteElement);
  element.addEventListener('click', (event) => {
    event.preventDefault();
    console.log(search);
    let jsonFileData = JSON.parse(localStorage[search]);
    chartListElement.innerHTML = '';
    loaderElement.classList.remove('hidden');
    loaderElement.innerHTML = loader;
    const chartElements = createElementsForCharts(jsonFileData.data);
    addElementsToDOM(chartElements);
    const charts = createCharts(jsonFileData.data);
    loaderElement.classList.add('hidden');
    // let data = totalData.find(x => x.search == search);
    console.log(jsonFileData.data);
  });
  return element;
};

const colors = randomColors(7);

const addElementsToDOM = (elements) => {
  elements.forEach((element) => {
    chartListElement.appendChild(element);
  });
};
const createCharts = (poiList) => {
  let chartsList = [];
  for (let poi in poiList) {
    chartsList.push(
      addDataToChart(poiList[poi].peakHours, poiList[poi].metaData)
    );
  }
  return chartsList;
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

const addDataToChart = (data, metaData) => {
  let title = metaData.title;
  let xValues = data['hours'];
  const id = createIDfromFileName(title);
  console.log(id);
  const chart = new Chart('' + id, {
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
        text: title + ' - ' + metaData.address,
        position: 'top',
      },
    },
  });
  return chart;
};

const createIDfromFileName = (fileName) => {
  return '' + fileName.split('/').pop().split('.').shift().replace(/ /g, '_');
};

const createElementsForCharts = (poiList) => {
  const elementList = [];
  // console.log(poiList)
  for (let poi in poiList) {
    elementList.push(createElementForChart(poiList[poi]));
  }
  return elementList;
};

const createElementForChart = (poi) => {
  const id = createIDfromFileName(poi.metaData.title);
  const div = document.createElement('canvas');
  div.id = id;
  div.classList.add('card');
  div.style = 'width:100%;max-width:700px';
  return div;
};

const scrapeWithQuery = async (query = 'Supermarkt%20Gent', amount = 5) => {
  let response = await fetch(
    `http://127.0.0.1:8000/rushhours/${query}/${amount}`
  );
  const jsonFile = await response.json();
  let jsonData = jsonFile.data;
  // totalData.push(jsonFile);
  // console.log(totalData)
  return jsonFile;
};

const getQueryParams = () => {
  try {
    const params = new Proxy(new URLSearchParams(window.location.search), {
      get: (searchParams, prop) => searchParams.get(prop),
    });
    console.log(params);
    // Get the value of "some_key" in eg "https://example.com/?some_key=some_value"
    let query = params.query; // "some_value"
    let amount = params.amount;
    if (query === null || query === '' || query === undefined) {
      // query = "Supermarkt%20Gent";
      throw new Error('No query given');
    }
    if (amount === '' || amount === null || amount === undefined) {
      amount = 5;
      // throw new Error('No amount given');
    }
    return { query, amount };
  } catch (e) {
    console.log(e);
  }
};

const createSidebarElementsFromLocalStorage = () => {
  const items = { ...localStorage };
  for (let key in items) {
    sidebarElement.appendChild(createElementForSidebar(key));
  }
};

window.onload = async() => {
  createSidebarElementsFromLocalStorage();
  const params = getQueryParams();
  if (params) {
    loaderElement.classList.remove('hidden');
    loaderElement.innerHTML = loader;
    const jsonFile = await scrapeWithQuery(params.query, params.amount);
    let search = params.query + ' ' + params.amount;
    saveToStorage(search, jsonFile);
    sidebarElement.appendChild(createElementForSidebar(search));
    const chartElements = createElementsForCharts(jsonFile.data);
    addElementsToDOM(chartElements);
    const charts = createCharts(jsonFile.data);
    loaderElement.classList.add('hidden');
  }
  
};

// const readTextFile = (file, callback) => {
//   var rawFile = new XMLHttpRequest();
//   rawFile.overrideMimeType('application/json');
//   rawFile.open('GET', file, true);
//   rawFile.onreadystatechange = function () {
//     if (rawFile.readyState === 4 && rawFile.status == '200') {
//       callback(rawFile.responseText);
//     }
//   };
//   rawFile.send(null);
// };

// const makeCharts = async () => {
//   // old version with json files
//   // jsonDataLinks.data.forEach(file => {
//   //   readTextFile(file, function (text) {
//   //     let data = JSON.parse(text);
//   //     // console.log(data)
//   //     for (let poi in data)
//   //     {
//   //       createElementForChart(data[poi]);
//   //       createChart(data[poi]);
//   //     }
//   //   });
//   // })
// };