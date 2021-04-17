package org.dengatherer.gatherer


import org.hamcrest.MatcherAssert.assertThat
import org.hamcrest.Matchers.`is`
import kotlin.test.Test

internal class ExposeParserTest {

    val json = """
        {
          "id": 1234567,
          "image": "https://example.com/apartment.jpg",
          "url": "https://example.com/apartment.html",
          "title": "A cozy apartment",
          "rooms": "2,5",
          "price": "819,50 €",
          "size": "86,03 m²",
          "address": "13351 Berlin (Wedding)",
          "crawler": "CrawlImmowelt"
        }
   """

    @Test
    fun `produces expose`() {
        ExposeParser().parse(json)
    }

    @Test
    fun `parses id`() {
        assertThat(ExposeParser().parse(json).id, `is`(1234567))
    }

    @Test
    fun `parses urls`() {
        val expose = ExposeParser().parse(json)
        assertThat(expose.image, `is`("https://example.com/apartment.jpg"))
        assertThat(expose.url, `is`("https://example.com/apartment.html"))
    }

    @Test
    fun `parses texts`() {
        val expose = ExposeParser().parse(json)
        assertThat(expose.title, `is`("A cozy apartment"))
        assertThat(expose.address, `is`("13351 Berlin (Wedding)"))
        assertThat(expose.crawler, `is`("CrawlImmowelt"))
    }

    @Test
    fun `parses rooms`() {
        val expose = ExposeParser().parse(json)
        assertThat(expose.rooms, `is`("2.5".toBigDecimal()))
    }

    @Test
    fun `parses price`() {
        val expose = ExposeParser().parse(json)
        assertThat(expose.price, `is`("819.50".toBigDecimal()))
    }

    @Test
    fun `parses size`() {
        val expose = ExposeParser().parse(json)
        assertThat(expose.size, `is`("86.03".toBigDecimal()))
    }
}

