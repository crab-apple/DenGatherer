package org.dengatherer.gatherer


import org.hamcrest.Matchers.allOf
import org.hamcrest.Matchers.containsString
import org.junit.jupiter.api.Test
import org.mockito.ArgumentMatcher
import org.mockito.Mockito.`when`
import org.mockito.Mockito.verify
import org.mockito.kotlin.argThat
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest
import org.springframework.boot.test.mock.mockito.MockBean
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.content
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.status
import java.time.Instant
import kotlin.reflect.KProperty1


@WebMvcTest(ExposeController::class)
internal class ExposeControllerTest {

    @Autowired
    private lateinit var mockMvc: MockMvc

    @MockBean
    private lateinit var exposeService: ExposeService

    @Test
    fun `returns exposes`() {

        fun expose(id: String) = Expose(
            id,
            "the-crawler",
            "the-url",
            "the-provider",
            "the-image",
            "expose-num-${id}",
            null,
            null,
            null,
            null,
            2.toBigDecimal(),
            700.toBigDecimal(),
            50.toBigDecimal(),
            null,
            null,
            Availability.new(Instant.parse("2022-02-02T02:02:02.222Z")),
        )

        `when`(exposeService.getAllExposes())
            .thenReturn(listOf(expose("e1"), expose("e2")))

        mockMvc.perform(get("/exposes"))
            .andExpect(
                content().string(
                    allOf(
                        containsString("e1"),
                        containsString("e2")
                    )
                )
            )
    }

    @Test
    fun `posts expose`() {

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
   """

        mockMvc.perform(
            post("/exposes")
                .contentType(MediaType.APPLICATION_JSON)
                .content(exposesJson)
        )


        verify(exposeService).notifyExpose(
            argThat(
                PropertyMatcher(ExposeInput::title, "A cozy apartment")
            )
        )
    }

    @Test
    fun `attempting to post a malformed expose results in a 400 error`() {

        val exposesJson = "[{}]"

        mockMvc.perform(
            post("/exposes")
                .contentType(MediaType.APPLICATION_JSON)
                .content(exposesJson)

        ).andExpect(status().isBadRequest)
    }
}

class PropertyMatcher<T, F>(private val property: KProperty1<T, F>, private val expectedValue: F) : ArgumentMatcher<T> {

    override fun matches(argument: T?): Boolean {
        return argument?.let(property) == expectedValue
    }

    override fun toString(): String {
        return "${property.name} should be [$expectedValue]"
    }
}