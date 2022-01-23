package org.dengatherer.gatherer

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/exposes", produces = ["application/json"])
class ExposeController(val exposeService: ExposeService) {

    @GetMapping()
    fun getExposes() = exposeService.getAllExposes()

    @PostMapping()
    fun postExpose(@RequestBody exposes: List<ExposeInput>) {
        for (expose in exposes) {
            exposeService.notifyExpose(expose)
        }
    }
}