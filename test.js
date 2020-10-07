const moment = require('moment')

var exp = moment.utc().add(1, 'h')

console.log(moment.utc().diff(exp))