package org.dengatherer.gatherer

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/exposes", produces = ["application/json"])
class ExposesController {

    @GetMapping()
    fun getExposes(): String {
        return "[]"
    }
}