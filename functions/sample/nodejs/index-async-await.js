/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');


 async function main(params) {
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });

     let selector = {};
     if (params.state) {
         selector.st = { '$eq': params.state };
     }

     const dbListPromise = await getDbs(cloudant, selector);
     return dbListPromise;
 }

 function getDbs(cloudant, selector={}) {
     return new Promise((resolve, reject) => {
         const db = cloudant.use('dealerships');
         db.find({ selector, use_index: '_design/st' })
         .then(result => {
             resolve({ dealerships: formatData(result) })
         })
         .catch(err => {
             reject({ err: err});
         });
     });
 }

  function formatData(result) {
     return result.docs.map((row) => {
         const doc = row;
         return {
             "id": doc.id,
             "city": doc.city,
             "state": doc.state,
             "st": doc.st,
             "address": doc.address,
             "zip": doc.zip,
             "lat": doc.lat,
             "long": doc.long
         }
     })
 }
