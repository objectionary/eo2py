package org.eolang;

import com.jcabi.log.Logger;
import org.apache.maven.plugin.testing.stubs.MavenProjectStub;
import org.cactoos.io.InputOf;
import org.cactoos.text.TextOf;
import org.hamcrest.MatcherAssert;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;

public final class CompileMojoTest {

    @Test
    public void testCreatesFinalXML() throws Exception {
        final Path temp = Files.createTempDirectory("eo");
        final Path src = temp.resolve("src");
        new Save("[args] > main\n  (stdout \"Hello!\").print > @\n", src.resolve("main.eo")).save();
        final Path target = temp.resolve("target");
        final Path generated = temp.resolve("generated");
        new Mojo<>(ParseMojo.class)
                .with("targetDir", target.toFile())
                .with("sourcesDir", src.toFile())
                .execute();
        new Mojo<>(OptimizeMojo.class)
                .with("targetDir", target.toFile())
                .execute();
        new Mojo<>(CompileMojo.class)
                .with("project", new MavenProjectStub())
                .with("targetDir", target.toFile())
                .with("generatedDir", generated.toFile())
                .execute();
        final Path finalXML = target.resolve("05-compile/main.eo.xml");
        MatcherAssert.assertThat(
                String.format("The file \"%s\" wasn't created", finalXML),
                Files.exists(finalXML),
                Matchers.is(true)
        );
        final String out = new TextOf(new InputOf(finalXML)).asString();
        Logger.info(this, "Java output:\n%s", out);
    }

}