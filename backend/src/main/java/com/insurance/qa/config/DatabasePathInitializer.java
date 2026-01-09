package com.insurance.qa.config;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import org.springframework.stereotype.Component;

@Component
public class DatabasePathInitializer {
  public DatabasePathInitializer() {
    try {
      Path dataPath = Paths.get("data");
      Files.createDirectories(dataPath);
    } catch (Exception ex) {
      throw new IllegalStateException("Failed to create data directory", ex);
    }
  }
}
