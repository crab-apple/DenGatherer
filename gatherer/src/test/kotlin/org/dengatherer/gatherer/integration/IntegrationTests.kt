package org.dengatherer.gatherer.integration

import io.restassured.RestAssured
import io.restassured.module.kotlin.extensions.Then
import io.restassured.module.kotlin.extensions.When
import org.apache.http.HttpStatus
import org.hamcrest.Matchers.`is`
import org.junit.jupiter.api.Test
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.web.server.LocalServerPort

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class IntegrationTests(@LocalServerPort val port: Int) {

    @Test
    fun `can read exposes`() {

        RestAssured.port = port

        When {
            get("/exposes")
        } Then {
            statusCode(HttpStatus.SC_OK)
            body(`is`("[]"))
        }
    }
}
