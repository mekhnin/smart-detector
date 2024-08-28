#* @apiTitle noise-reduction-server API

#* @param width:int
#* @param height:int
#* @param lw:int
#* @param lh:int
#* @post /decompose
function(req, width, height, lw, lh){
    data <- matrix(as.numeric(jsonlite::fromJSON(req$postBody)),
                   nrow = as.numeric(height),
                   ncol = as.numeric(width),
                   byrow = TRUE)
    s <- Rssa::ssa(data, svd.method = 'auto', kind = '2d-ssa', L = c(as.numeric(lw), as.numeric(lh)))
    gr <- Rssa::grouping.auto(s, grouping.method = 'wcor', method = 'average', nclust = 2)
    attr(Rssa::reconstruct(s, groups = list(gr[[2]])), 'residuals')
}

#* @get /ping
function(){
    'OK'
}
