irk_kind_predicates <- list(
    Image = function(value) {
        inherits(value, "irk_image") &&
            is.list(value) &&
            is.matrix(value$pixels) &&
            is.numeric(value$width) && length(value$width) == 1L &&
            !is.na(value$width) && is.finite(value$width) &&
            value$width == floor(value$width) &&
            is.numeric(value$height) && length(value$height) == 1L &&
            !is.na(value$height) && is.finite(value$height) &&
            value$height == floor(value$height) &&
            value$width == ncol(value$pixels) &&
            value$height == nrow(value$pixels)
    },
    Table = function(value) is.data.frame(value) || is.matrix(value),
    Text = function(value) is.character(value),
    Number = function(value) is.numeric(value),
    Model = function(value) inherits(value, c("lm", "glm"))
)

irk_image <- function(pixels) {
    if (!is.matrix(pixels)) {
        stop("irk_image needs a pixel matrix", call. = FALSE)
    }
    structure(
        list(pixels = pixels, width = ncol(pixels), height = nrow(pixels)),
        class = "irk_image"
    )
}

irk_expect_kind <- function(value, kind, where) {
    predicate <- irk_kind_predicates[[kind]]
    if (is.null(predicate)) {
        stop(sprintf("IRK does not know the kind %s", kind), call. = FALSE)
    }
    if (!predicate(value)) {
        stop(sprintf("%s must be %s", where, kind), call. = FALSE)
    }
    invisible(value)
}
