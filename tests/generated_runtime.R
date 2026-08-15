arguments <- commandArgs(trailingOnly = TRUE)
source(arguments[[1]])

pixels <- matrix(seq_len(24L), nrow = 4L, ncol = 6L)
image <- irk_image(pixels)
result <- downsize_image(image)

stopifnot(
    inherits(result, "irk_image"),
    result$width == 3L,
    result$height == 2L,
    identical(result$pixels, pixels[c(1L, 3L), c(1L, 3L, 5L), drop = FALSE])
)

wrong_kind <- try(downsize_image(data.frame(x = 1L)), silent = TRUE)
stopifnot(inherits(wrong_kind, "try-error"))

forged <- irk_image(pixels)
forged$width <- 6.9
wrong_structure <- try(downsize_image(forged), silent = TRUE)
stopifnot(inherits(wrong_structure, "try-error"))
