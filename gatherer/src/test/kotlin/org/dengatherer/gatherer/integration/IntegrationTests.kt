package org.dengatherer.gatherer.integration

import io.restassured.RestAssured
import io.restassured.http.ContentType
import io.restassured.module.kotlin.extensions.Then
import io.restassured.module.kotlin.extensions.When
import org.apache.http.HttpStatus
import org.dengatherer.gatherer.ExposeService
import org.hamcrest.Matchers.`is`
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.web.server.LocalServerPort

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class IntegrationTests {

    @Autowired
    private lateinit var exposeService: ExposeService

    @BeforeEach
    fun clearData() {
        exposeService.clearExposes()
    }

    @BeforeEach
    fun setupRestAssured(@LocalServerPort port: Int) {
        RestAssured.port = port
    }

    @Test
    fun `exposes can be listed through HTTP`() {

        When {
            get("/exposes")
        } Then {
            statusCode(HttpStatus.SC_OK)
            contentType(ContentType.JSON)
            body(`is`("[]"))
        }
    }

    @Test
    fun `can be notified of exposes`() {

        val exposeJson = """
            {
              "id": 1234567,
              "image": "https://example.com/apartment.jpg",
              "url": "https://example.com/apartment.html",
              "title": "A cozy apartment",
              "rooms": "2",
              "price": "819,50 €",
              "size": "86,03 m²",
              "address": "13351 Berlin (Wedding)",
              "crawler": "CrawlImmowelt"
            }
        """.trimIndent()

        RestAssured.given().body(exposeJson)
            .post("/exposes")

        When {
            get("/exposes")
        } Then {
            statusCode(HttpStatus.SC_OK)
            contentType(ContentType.JSON)
            body("[0].title", `is`("A cozy apartment"))
        }
    }
}
