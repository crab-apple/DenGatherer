package org.dengatherer.gatherer

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class ExposesController {

    @GetMapping("/exposes")
    fun getExposes(): String {
        return "[]"
    }
}