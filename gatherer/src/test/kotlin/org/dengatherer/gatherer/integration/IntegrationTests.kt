package org.dengatherer.gatherer.integration

import io.restassured.RestAssured
import io.restassured.RestAssured.given
import io.restassured.http.ContentType
import io.restassured.module.kotlin.extensions.Then
import io.restassured.module.kotlin.extensions.When
import org.apache.http.HttpStatus
import org.dengatherer.gatherer.ExposeDAO
import org.dengatherer.gatherer.InMemoryExposeDAO
import org.hamcrest.Matchers.`is`
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.web.server.LocalServerPort
import org.springframework.test.context.ActiveProfiles

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class IntegrationTests {

    @Autowired
    private lateinit var exposeDAO: InMemoryExposeDAO

    @BeforeEach
    fun clearData() {
        exposeDAO.clearExposes()
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

        val exposesJson = """
            [{
              "id": "1234567",
              "image": "https://example.com/apartment.jpg",
              "url": "https://example.com/apartment.html",
              "title": "A cozy apartment",
              "rooms": "2.5",
              "coldRent": "819.50",
              "size": "86.03",
              "address": "13351 Berlin (Wedding)",
              "source": "CrawlImmowelt"
            }]
        """.trimIndent()

        given()
            .contentType(ContentType.JSON)
            .body(exposesJson)
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
