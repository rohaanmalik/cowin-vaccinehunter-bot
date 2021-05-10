var axios = require('axios');

var config = {
  method: 'get',
  url: 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=365&date=12-05-2021\n',
  headers: { }
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});
