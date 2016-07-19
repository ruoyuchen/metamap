var ROOT_PATH = require('x-root-path');

var common = require( ROOT_PATH + '/utils/common');

module.exports = function (router) {

    router.get('/list', function (req, res) {
      common.getRequest({
            urlsName:'allMeta',
            req: req,
            params: req.query
          }, function (metas) {
            res.render('meta/list', { metas : metas});
          })
    });

    router.get('/col_seach', function (req, res) {
      common.getRequest({
            urlsName:'searchCol',
            req: req,
            params: req.query
          }, function (cols) {
            res.render('meta/col_seach', { cols : cols, colName: req.query.colName});
          })
    });

    router.get('/tblinfo', function (req, res) {
      common.getRequest({
            urlsName:'getTableInfo',
            req: req,
            params: req.query
          }, function (data) {
            var tbl = data.tbl;
            var cols = data.cols;
            console.log('tbl is : ' + JSON.parse(tbl));
            tbl.createTime = common.formatDate(new Date(tbl.create_time * 1000), 'yymmdd hh:mm:ss');
            res.render('meta/tbl', { cols : cols, tbl: tbl});
          })
    });

    router.get('/add', function (req, res) {
      res.render('meta/edit');
    });

    router.post('/add', function (req, res) {
      common.postFormRequest({
        urlsName: 'addMeta',
        req: req,
        form: req.body
      }, function (results) {
        if (results.message == 'success') {
          console.log(req.body.meta + ' has been added');
          res.redirect("list");
        } else {
          res.send(results);
        }
      });
    });

    router.get('/edit', function (req, res) {
      common.getRequest({
        urlsName:'editMeta',
        req: req,
        params: req.query
      }, function (meta) {
        console.log("done with " + meta.id);
        meta.ctimeFormat = common.formatDate(new Date(meta.ctime), 'yymmdd hh:mm:ss');
        res.render('meta/edit', { meta_obj : meta });
      })
    });
};