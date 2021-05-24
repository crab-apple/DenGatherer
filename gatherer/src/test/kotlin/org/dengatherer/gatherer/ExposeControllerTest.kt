package org.dengatherer.gatherer


import org.hamcrest.Matchers.allOf
import org.hamcrest.Matchers.containsString
import org.junit.jupiter.api.Test
import org.mockito.Mockito.`when`
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest
import org.springframework.boot.test.mock.mockito.MockBean
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.content


@WebMvcTest(ExposeController::class)
internal class ExposeControllerTest {

    @Autowired
    private lateinit var mockMvc: MockMvc

    @MockBean
    private lateinit var exposeService: ExposeService

    @Test
    fun `returns exposes`() {
        `when`(exposeService.getAllExposes())
            .thenReturn(listOf(expose(1), expose(2)))

        mockMvc.perform(get("/exposes"))
            .andExpect(
                content().string(
                    allOf(
                        containsString("expose-num-1"),
                        containsString("expose-num-2")
                    )
                )
            )
    }

    private fun expose(id: Int) = Expose(
        id,
        "the-image",
        "the-url",
        "expose-num-${id}",
        2.toBigDecimal(),
        700.toBigDecimal(),
        50.toBigDecimal(),
        "the address",
        "the crawler"
    )
}