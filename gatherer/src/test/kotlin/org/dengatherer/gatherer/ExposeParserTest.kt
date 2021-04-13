package org.dengatherer.gatherer


import org.hamcrest.MatcherAssert.assertThat
import org.hamcrest.Matchers.equalTo
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
        assertThat(
            ExposeParser().parse(json).id,
            equalTo(1234567)
        )
    }
}

